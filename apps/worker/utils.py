import time
from django.core.cache import cache
from apps.worker.models import TaskJob
from django.contrib.auth import get_user_model
from apps.generator.gemini.gemini_repositories import gemini_flash_2_0_quiz_generator,gemini_flash_2_0_flashcard_generator,gemini_flash_2_0_flashcard_auto_generator
from apps.generator.file_reader import extract_text_from_file
from apps.s3_buckets.supabase_storage import download_file
from datetime import timedelta
from django.utils import timezone
from apps.generator.utils import check_generative_ai_usage

def start_worker():
    """
    Poll the database for pending tasks.
    This worker function sets a cache flag, processes tasks, and then clears the flag.
    """
    # Set a flag in the cache so we know a worker is running (expires in 10 minutes, adjust as needed)
    cache.set('worker_running', True, timeout=5000)
    cleanup_old_tasks()
    try:
        while True:
            pending_jobs = TaskJob.objects.filter(status='PENDING')
            if not pending_jobs.exists():
                # No pending jobs, so break the loop and stop the worker.
                break
            for job in pending_jobs:
                cache.set('worker_running', True, timeout=5000)
                # Atomically mark the job as processing to avoid duplicate processing.
                updated = TaskJob.objects.filter(pk=job.pk, status='PENDING').update(status='PROCESSING')
                if updated == 1:
                    payload = job.payload
                    user_id = payload.get('user_id')
                    target_id = payload.get('target_id')
                    num_questions = payload.get('num_questions')
                    difficulty = payload.get('difficulty')
                    requested_ai_model = payload.get('requested_ai_model')
                    should_make_flashcard = payload.get('should_make_flashcard')
                    file_name = payload.get('file_name')
                    
                    try:
                        file_content = None
                        # If a file_name exists, download and process the file to extract text.
                        if file_name:
                            downloaded_file = download_file(file_name, bucket_name="generator-input-files")
                            downloaded_file.name = file_name
                            file_content = extract_text_from_file(downloaded_file)
                            check_generative_ai_usage(user_id,num_questions,file_content)
                            
                        
                        if requested_ai_model == "Gemini-flash-2" and job.task_type == "quiz_file":
                            User = get_user_model()
                            user = User.objects.get(pk=user_id)
                            result = gemini_flash_2_0_quiz_generator(
                                user,
                                quiz_id=target_id,
                                num_questions=num_questions,
                                difficulty=difficulty,
                                notes=file_content  # Pass the extracted text as notes.
                            )
                            #for aut generate flashcard
                            if should_make_flashcard:
                                gemini_flash_2_0_flashcard_auto_generator(target_id, num_questions)
                            
                            job.result = result
                            job.status = 'SUCCESS'

                        elif requested_ai_model == "Gemini-flash-2" and job.task_type == "flashcard_file":
                            User = get_user_model()
                            user = User.objects.get(pk=user_id)
                            result = gemini_flash_2_0_flashcard_generator(
                                user,
                                flashcard_id=target_id,
                                num_questions=num_questions,
                                difficulty=difficulty,
                                notes=file_content  # Pass the extracted text as notes.
                            )
                            job.result = result
                            job.status = 'SUCCESS'
                        else:
                            job.result = f"Unsupported AI model: {requested_ai_model}"
                            job.status = 'FAILED'
                    except Exception as e:
                        job.result = str(e)
                        job.status = 'FAILED'
                    job.save()
            # Sleep for a short interval before checking again.
            time.sleep(5)
    finally:
        # Remove the flag when done.
        cache.delete('worker_running')

def cleanup_old_tasks():
    try:
        cutoff = timezone.now() - timedelta(hours=24)
        tasks_to_delete = TaskJob.objects.filter(created_at__lt=cutoff).exclude(status='PENDING')
        count = tasks_to_delete.count()
        tasks_to_delete.delete()
    except Exception as e:
        pass