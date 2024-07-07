package domain

type UserRole int

const (
	UserBreeder = iota
	UserJudge
	UserOrganiser
)

type User struct {
	Id             ID
	Email          Email
	Name           UserName
	HashedPassword string
	Role           UserRole
}
