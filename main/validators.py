import re
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

special_character_regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')


def SpecialCharacterValidator(value):           

    if special_character_regex.search(value):
            raise ValidationError(
                _('Special Characters not allowed in username and name.'),
                params={'value': value},)

