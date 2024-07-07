package domain

import (
	"net/mail"

	"time"

	log "github.com/sirupsen/logrus"
)

type Email string

func (email Email) String() string {
	return string(email)
}

func NewEmail(email string) Email {
	e, err := mail.ParseAddress(email)
	if err != nil {
		log.WithFields(log.Fields{
			"from":    "EmailServiceStart",
			"problem": "GetNoNotifiedOrderShops",
		}).Error(err.Error())
		time.Sleep(time.Minute)
	}

	return Email(e.Address)
}
