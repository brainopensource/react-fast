backend/
├── .env                       # Environment variables
├── CHANGELOG.md               # Change log of the project
├── config/                    # Configuration files
├── main.py                    # Entry point of the application
├── poetry.lock                # Poetry lock file
├── pyproject.toml             # Poetry configuration file
├── README.md                  # Project README file
├── references_brainstorm.txt  # Brainstorming references
├── requirements.txt           # Project dependencies
├── app/
│   ├── adapters/                # Implementations of driven ports (e.g., database repositories, API clients)
│   │   ├── api_clients/         # External API clients
│   │   ├── http_adapters/       # HTTP adapters
│   │   │   └── http_client.py
│   │   ├── processors/          # Data processors
│   │   ├── repositories/        # Database repositories
│   │   └── task_queue/          # Task queue adapters
│   ├── application/           # Application layer (use cases and application services)
│   │   ├── dtos/                # Data transfer objects
│   │   │   └── external_data_dto.py
│   │   ├── services/            # Application services
│   │   ├── use_cases/           # Use case implementations
│   │   │   ├── fetch_external_data.py
│   │   │   └── get_greeting.py
│   ├── domain/                # Core domain logic (entities, value objects, interfaces)
│   │   ├── entities/            # Domain entities
│   │   │   └── message.py
│   │   ├── interfaces/          # Domain interfaces
│   │   │   └── http_interfaces/
│   │   │       └── external_service.py
│   │   └── value_objects/       # Value objects
│   ├── infrastructure/        # Infrastructure concerns (e.g., database connections, DI container)
│   │   ├── database/            # Database configuration
│   │   ├── di/                  # Dependency injection container
│   │   │   └── container.py
│   │   ├── logging/             # Logging configuration
│   │   ├── messaging/           # Messaging infrastructure
│   │   └── settings/            # Application settings
│   ├── presentation/          # Presentation layer (driving adapters)
│   │   ├── api/                 # REST API controllers and setup
│   │   │   ├── api_setup.py
│   │   │   └── rest_controllers/
│   │   │       ├── external_data_controller.py
│   │   │       └── greeting_controller.py
│   │   ├── cli/                 # Command-line interface
│   │   └── converters/          # Data converters
├── docs/
│   ├── api_documentation.md
│   ├── deployment_guide.md
│   ├── development_plan.md
│   ├── features_imlpementation.md
│   ├── modules_descriptions.md
│   ├── optimization_guide.md
│   ├── project_principles.md
│   ├── project_review.md
│   ├── project_structure.md
│   ├── restructure_plan.md
│   ├── roadmap.md
│   ├── security_considerations.md
│   ├── testing_plan.md
│   └── user_guide.md
│   └── ignore/
│       └── old_code.md
├── scripts/                   # Script files
├── tests/                     # Test files
│   ├── evolve/
│   ├── integration/
│   └── unit/
