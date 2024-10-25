
# Example of social_user_custom pipeline function
from social_core.pipeline.social_auth import social_user
from customerlogin.models import Customer


def social_user_custom(strategy, details, backend, uid, user=None, *args, **kwargs):
    email = details.get('email')
    if email:
        try:
            user_obj = Customer.objects.get(email=email)
            return {
                'user': user_obj,
                'is_new': False
            }
        except Customer.DoesNotExist:
            pass

    # Call social_user function with correct arguments
    return social_user(strategy, details, backend, uid, *args, **kwargs)


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        email = response.get('email')
        first_name = response.get('given_name')
        last_name = response.get('family_name')

        if email:
            customer, created = Customer.objects.get_or_create(email=email)
            if created:
                customer.first_name = first_name
                customer.last_name = last_name
                customer.save()
            return {'is_new': created, 'user': customer}
