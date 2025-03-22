# Rockae Backend Database Schema

## Overview
The backend database is a fully functionaly postgre sql

## Database Schema

### User Table
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `id` | Integer | Primary Key, Auto-increment |
| `user_id` | CharField | Unique, Format: ADM<pk> or USR<pk> |
| `username` | varchar(255) | Unique, NOT NULL |
| `email` | varchar | Unique, NOT NULL |
| `password` | varchar | NOT NULL |
| `is_verified` | boolean | default: false |
| `is_active` | boolean | default: true |
| `date_joined` | datetime | auto-generated |

### UserProfile Table
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `id` | Integer | PRIMARY KEY, AUTO_INCREMENT |
| `user` | ForeignKey | REFERENCES User (user_id), UNIQUE |
| `firstname` | varchar | |
| `lastname` | varchar | |
| `phone_number` | varchar | nullable |
| `photo` | file | nullable |

### Quiz Table
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `id` | int | PRIMARY KEY |
| `quiz_title` | varchar | NOT NULL |
| `description` | text | nullable |
| `user` | int | FOREIGN KEY REFERENCES User (user_id) |
| `create_date` | datetime | auto-generated |
| `number_of_questions` | int | default: 10 |
| `difficulty_level` | varchar | Choices: Easy, Medium, Hard |
| `category` | varchar | NOT NULL |
| `is_public` | boolean | default: false |
| `is_timed` | boolean | default: false |
| `time_limit` | float | nullable |
| `auth_required` | boolean | default: false |
| `has_flash_card` | boolean | default: false |

### Question Table
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `id` | int | PRIMARY KEY |
| `quiz_id` | int | ForeignKey to Quiz |
| `text` | text | NOT NULL |

### AnswerOption Table
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `id` | int | PRIMARY KEY |
| `question_id` | int | ForeignKey to Question |
| `label` | varchar(1) | NOT NULL (A, B, C, D, etc.) |
| `text` | text | NOT NULL |
| `is_correct` | boolean | NOT NULL |

### Flashcard Table
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `id` | int | PRIMARY KEY |
| `title` | varchar | NOT NULL |
| `description` | text | nullable |
| `user_id` | int | ForeignKey to User |
| `quiz_id` | int | One-to-one relationship with Quiz, nullable |

### FlashcardItem Table
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `id` | int | PRIMARY KEY |
| `flashcard_id` | int | ForeignKey to Flashcard |
| `question` | text | NOT NULL |
| `answer` | text | NOT NULL |

### SubscriptionPlan Table
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `id` | int | PRIMARY KEY |
| `name` | varchar | UNIQUE, NOT NULL |
| `duration_days` | int | NOT NULL |
| `price` | decimal | NOT NULL |
| `is_active` | boolean | default: true |

### UserSubscription Table
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `id` | int | PRIMARY KEY |
| `user_id` | int | ForeignKey to User |
| `plan_id` | int | ForeignKey to SubscriptionPlan |
| `start_date` | datetime | auto-generated |
| `end_date` | datetime | calculated from SubscriptionPlan |

## API Endpoints

(Endpoints listed as previously defined)

## Technologies
- **Django**
- **Django REST Framework**
- **JWT Authentication**
- **Pandas (CSV/Excel processing)**
- **DRF Spectacular (API documentation)**
- **Generative AI (Gemini)**
- **Decouple (Environment Variables Management)**
- **Corsheaders (Cross-Origin Resource Sharing)**

## Security Measures
- **JWT Authentication**
- **Custom Permission Classes**
- **Data Validation & Sanitization**
- **Error Handling & Standardized Responses**
- **File Upload Security**
- **FTP Secure Storage**

## Deployment
- Uses FTP storage for handling static and user-uploaded files
- Environment configuration via `python-decouple`
- Ready for deployment to platforms such as Railway, Heroku, or AWS

## Documentation
- Comprehensive API documentation via DRF Spectacular (Swagger/OpenAPI)

## Configuration
- Secure environment variables handling (`SECRET_KEY`, `DATABASE_URL`, SMTP settings, AI keys)
- Database configured for optimized production performance (`dj_database_url`)
- JWT authentication token lifetime configurable

## Future Enhancements
- Real-time analytics
- Enhanced admin interface
- User activity logs
- Expanded subscription and payment options

