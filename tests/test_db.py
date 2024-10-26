from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='davkuk',
        email='davkuk@example.com',
        password='todolist_2',
    )
    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'davkuk@example.com')
    )

    assert result.id == 1
    assert result.username == 'davkuk'
    assert result.email == 'davkuk@example.com'
