from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    # 일반 user 생성, username 이 userID를 의미함
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("Users must have an userID.")
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 User 생성
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = UserManager()  # 헬퍼 클래스 사용

    USERNAME_FIELD = 'username'  # 로그인 ID로 사용할 필드
    REQUIRED_FIELDS = ['email']  # 필수 작성 필드
