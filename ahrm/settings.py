# Django settings for ahrm project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'ahrm.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
gettext = lambda s: s
LANGUAGE_CODE = 'km'

LANGUAGES = (
             ('en', gettext('English')),
             ('km', gettext('Khmer')),
            
)


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'site_media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%m3cg_&3!ns463s_c#6ok5@=iq198w4&1(+o-w6941pqnv*5a7'

'''
TinyMCE configuration
'''
TINYMCE_JS_URL = '/site_media/javascripts/tiny_mce/tiny_mce.js' #The URL of the TinyMCE javascript file.
TINYMCE_JS_ROOT = '/site_media/javascripts/tiny_mce' #The filesystem location of the TinyMCE files.
TINYMCE_DEFAULT_CONFIG = {
                          'plugins': "table,spellchecker,paste,searchreplace,inlinepopups,preview,safari",
                          'theme': "advanced",
                          'mode': "textareas",
                          'skin' : "o2k7",
                          'language': "{{ language }}",
                          'spellchecker_languages' : "{{ spellchecker_languages }}",
                          'spellchecker_rpc_url' : "{{ spellchecker_rpc_url }}",
                          'theme_advanced_buttons1' : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontselect,fontsizeselect",
                          'theme_advanced_buttons2' : "pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
                          'theme_advanced_toolbar_location' : "top",
                          'theme_advanced_toolbar_align' : "left",
                          'force_br_newlines' : "true",
                          'force_p_newlines' : "false",
                          'theme_advanced_resizing' : "false", 
                          'content_css' : "/site_media/style.css",
                          #'file_browser_callback' : "fileBrowser" 
                          }  #The default TinyMCE configuration to use. See the TinyMCE manual for all options. To set the configuration for a specific TinyMCE editor, see the mce_attrs parameter for the widget.

TINYMCE_SPELLCHECKER = False #Whether to use the spell checker through the supplied view. You must add spellchecker to the TinyMCE plugin list yourself, it is not added automatically.
TINYMCE_COMPRESSOR = False #Whether to use the TinyMCE compressor, which gzips all Javascript files into a single stream. This makes the overall download size 75% smaller and also reduces the number of requests. The overall initialization time for TinyMCE will be reduced dramatically if you use this option.


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',

)

ROOT_URLCONF = 'ahrm.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # DOM: why not use relative paths?
    'templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'tinymce',
    'ahrm.main'
    
)
