"""factory-boy factory for the custom user model."""

import factory
from django.contrib.auth import get_user_model

DEFAULT_TEST_PASSWORD = "Str0ng-Test-Passw0rd!"


class UserFactory(factory.django.DjangoModelFactory):
    """Build ``accounts.User`` instances for tests."""

    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)

    email = factory.Sequence(lambda index: f"user{index}@example.com")
    full_name = factory.Faker("name")
    phone = factory.Sequence(lambda index: f"+92300{index:07d}")
    is_active = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Assign a usable password to every generated user."""

        self.set_password(extracted or DEFAULT_TEST_PASSWORD)
        if create:
            self.save(update_fields=["password"])
