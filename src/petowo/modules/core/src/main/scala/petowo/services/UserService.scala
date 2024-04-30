package petowo.services


import cats._

trait UserService[F[_]] {
  def get(id: UserId): F[User]
  def getByName(name: Username): F[User]
  def delete(id: UserId, authed: UserId): F[Unit]
}
//(repo: UserRepository[F], iam: IAMService[F])
object UserService {
  def make[F[_]: MonadThrow]: UserService[F] =
    new UserServiceImpl()

  private final class UserServiceImpl[F[_]: MonadThrow] extends UserService[F] {
    override def getByName(name: Any): F[Any] =
      "getByName"
      
    override def get(id: UserId): F[User] =
      "get"
      
    override def delete(id: UserId, authed: UserId): F[Unit] = 
      "delete"
  }
}