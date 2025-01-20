from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует",
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неправильная почта или пароль",
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истёк",
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен отсутствует",
)

IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена",
)

UserDoesntExistException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
)

InsufficientPermissionsException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Недостаточно прав для получения доступа",
)

ReturnTimeBeforeLendTimeException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Время возврата книги раньше времени выдачи",
)

BookNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Нет книги с таким ID",
)

BookAlreadyLentException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Эта книга уже взята",
)

NoBooksLeftException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="В наличии нет книг с таким ID",
)

FiveBooksLentException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Вы уже взяли 5 книг, это лимит",
)

UserDoesntHaveThisBookException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="У вас нет книги с таким ID",
)
