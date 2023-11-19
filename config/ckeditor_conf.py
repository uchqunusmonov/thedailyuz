configs = {
    'default': {
        'skin': 'moono',
        'toolbar_Basic': [
            ['Bold', 'Italic', 'Underline']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Bold', 'Italic']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'Undo', 'Redo']},
            {'name': 'insert', 'items': ['Link', 'Unlink', 'HorizontalRule']},
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'tools', 'items': ['Maximize']},
            {'name': 'about', 'items': ['About']},
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'autolink',
            'autoembed',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'elementspath'
        ]),
    }
}
