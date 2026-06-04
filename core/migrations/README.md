# LUPPI 3.0 Database Migrations

## New Models

The following models have been added for LUPPI 3.0 advanced memory:

1. **LuppiConversation** - Stores conversation sessions
2. **LuppiConversationTurn** - Stores individual message turns
3. **LuppiUserProfile** - Stores user preferences and goals
4. **LuppiEmotionalPattern** - Tracks emotional patterns over time
5. **LuppiDomainFrequency** - Tracks domain usage frequency

## Migration Instructions

Run the following commands to create and apply migrations:

```bash
python manage.py makemigrations core
python manage.py migrate
```

## Model Details

### LuppiConversation
- user (ForeignKey to User, nullable for anonymous)
- session_key (CharField, for anonymous users)
- provider (CharField: local, anthropic, gemini)
- started_at (DateTimeField)
- ended_at (DateTimeField, nullable)
- turn_count (IntegerField)
- primary_domain (CharField)
- is_active (BooleanField)

### LuppiConversationTurn
- conversation (ForeignKey to LuppiConversation)
- role (CharField: user, assistant)
- content (TextField)
- domain (CharField)
- emotion (CharField)
- insight_id (CharField, nullable)
- intent (CharField, nullable)
- confidence (FloatField, nullable)
- created_at (DateTimeField)

### LuppiUserProfile
- user (OneToOne to User)
- preferred_language (CharField, default: hi-en)
- preferred_response_style (CharField)
- goals (JSONField)
- struggles (JSONField)
- interests (JSONField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### LuppiEmotionalPattern
- user (ForeignKey to User, nullable)
- session_key (CharField, nullable)
- emotion (CharField)
- intensity (FloatField)
- domain (CharField)
- timestamp (DateTimeField)

### LuppiDomainFrequency
- user (ForeignKey to User, nullable)
- session_key (CharField, nullable)
- domain (CharField)
- count (IntegerField)
- last_accessed (DateTimeField)

## Indexes

All models have appropriate indexes for performance:
- user field for user-based queries
- session_key for anonymous user queries
- timestamp for time-based queries
- domain for domain-based queries
