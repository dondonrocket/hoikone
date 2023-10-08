from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_no_numeric_password(value):
    if value.isdigit():
        raise ValidationError(_("パスワードに数字だけの文字列は使用できません。"))
