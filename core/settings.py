"""Global Project Configurations."""

from pathlib import Path
import os
import sys
import environ
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
from decouple import config
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env("core/.env")
ENVIRONMENT = env

SECRET_KEY = os.environ.get("SECRET_KEY", default="your secret key")

# DEBUG = "RENDER" not in os.environ
DEBUG = True

ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "users",
    "core",
    "home",
    "products",
    "cart",
    "management",
    "payment",
]

THIRD_PARTY_APPS = [
    "paypal.standard.ipn",
    "import_export",
    "cloudinary",

     'django_ckeditor_5',

        # Other installed apps
    'django.contrib.sites',  # Required by allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # For Google OAuth
   'allauth.socialaccount.providers.facebook',

    'mptt',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

SITE_ID = 1


PAYPAL_RECEIVER_EMAIL = "sb-bjeh4728354490@business.example.com"
PAYPAL_TEST = True
PAYPAL_BUY_BUTTON_IMAGE = "/static/img/buttom_paypal.svg"

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
     # Add the AccountMiddleware from django-allauth
    'allauth.account.middleware.AccountMiddleware',

]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "utils.context_processors.company",
                "utils.context_processors.user_preferences",
                "utils.context_processors.products_featured",
                "utils.context_processors.products_categories",
                "utils.context_processors.categories_tree",
                "utils.context_processors.cart_items_count",


            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# if "test" in sys.argv:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
    }
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": env("DB_NAME"),
#             "USER": env("DB_USER"),
#             "PASSWORD": env("DB_PASSWORD"),
#             "HOST": env("DB_HOST"),
#             "PORT": env("DB_PORT"),
#             "ATOMIC_REQUESTS": True,
#         }
#     }

AUTH_USER_MODEL = "users.CustomUser"

LOGIN_URL = "/users/login/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",

    # for django all-auth backend for google
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth backend



]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = "/media/"

cloudinary.config(
    cloud_name=env("CLOUDINARY_CLOUD_NAME"),
    api_key=env("CLOUDINARY_API_KEY"),
    api_secret=env("CLOUDINARY_API_SECRET"),
    secure=True,
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# X_FRAME_OPTIONS = 'ALLOW-FROM http://127.0.0.1:8000'
X_FRAME_OPTIONS = 'SAMEORIGIN'
CSP_FRAME_ANCESTORS = ["'self'", "http://127.0.0.1:8000"]

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    DATABASES = {
        "default": dj_database_url.config(
            default="postgresql://postgres:postgres@localhost:5432/mysite",
            conn_max_age=600,
        )
    }



#...


####################################
    ##  CKEDITOR CONFIGURATION ##
####################################

customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
    ]

# CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
# CKEDITOR_5_FILE_STORAGE = os.path.join(BASE_DIR, 'media', "ckeditor") # optional
CKEDITOR_5_CONFIGS = {
'default': {
    'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

},
'extends': {
    'blockToolbar': [
        'paragraph', 'heading1', 'heading2', 'heading3',
        '|',
        'bulletedList', 'numberedList',
        '|',
        'blockQuote',
    ],
    'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
    'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                'insertTable',],
    'image': {
        'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                    'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
        'styles': [
            'full',
            'side',
            'alignLeft',
            'alignRight',
            'alignCenter',
        ]

    },
    'table': {
        'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
        'tableProperties', 'tableCellProperties' ],
        'tableProperties': {
            'borderColors': customColorPalette,
            'backgroundColors': customColorPalette
        },
        'tableCellProperties': {
            'borderColors': customColorPalette,
            'backgroundColors': customColorPalette
        }
    },
    'heading' : {
        'options': [
            { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
            { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
            { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
            { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
        ]
    }
},
'list': {
    'properties': {
        'styles': 'true',
        'startIndex': 'true',
        'reversed': 'true',
    }
}
}

# Define a constant in settings.py to specify file upload permissions
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"  # Possible values: "staff", "authenticated", "any"





# print(os.environ.get("CLIENT_ID"))
# print(os.environ.get("CLIENT_SECRET"))

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],

        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
         'APP': {
            'client_id': os.environ.get("CLIENT_ID"),
            'secret': os.environ.get("CLIENT_SECRET"),
            'key': ''
        }
    },
    'facebook': {
            'METHOD': 'oauth2',  # Facebook uses OAuth2
            'SCOPE': ['email', 'public_profile'],  # Permissions requested from the user
            'AUTH_PARAMS': {'auth_type': 'reauthenticate'},  # Optional, reauthenticate if needed
            'FIELDS': [
                'id',
                'email',
                'name',
                'first_name',
                'last_name',
                'verified',
                'locale',
                'timezone',
                'link',
                'gender',
                'updated_time',
            ],
            'EXCHANGE_TOKEN': True,  # Exchange the short-lived token for a long-lived one
            'LOCALE_FUNC': lambda request: 'en_US',  # Default locale setting
            'VERIFIED_EMAIL': False,  # Set True if you require verified email
            'VERSION': 'v12.0',  # Facebook API version, change based on their latest
            'APP': {
                'client_id': os.environ.get("FACEBOOK_CLIENT_ID"),
                'secret': os.environ.get("FACEBOOK_CLIENT_SECRET"),
                'key': ''
            }
        }
}



LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Allauth settings
ACCOUNT_EMAIL_VERIFICATION = "none"  # Disable email verification for demo

# with social-auth-app-django google authentication



# with social-auth-app-django google authentication

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("CLIENT_ID")
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("CLIENT_SECRET")
# SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://127.0.0.1:8000/complete/google/'  # Use your domain in production
# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']

# SOCIAL_AUTH_URL_NAMESPACE = 'social'


# with social-auth-app-django facebook authentication

