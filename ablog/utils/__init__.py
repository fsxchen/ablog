'''
Author: yangxingchen
Date: 2021-02-04 11:10:30
LastEditors: yangxingchen
LastEditTime: 2021-02-04 11:10:44
Description: 
'''

# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)
