package domain

type UserName string

func (name UserName) String() string {
	return string(name)
}

func NewUserName(name string) UserName {
	return UserName(name)
}
