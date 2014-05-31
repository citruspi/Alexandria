package main

import (
	"fmt"
	"net/http"

	"github.com/go-martini/martini"
	"github.com/martini-contrib/render"
	"labix.org/v2/mgo"
	"labix.org/v2/mgo/bson"
)

type User struct {
	Id            bson.ObjectId `bson:"_id"              json:"-"`
	Username      string        `bson:"username"         json:"username"`
	Realname      string        `bson:"realname"         json:"realname"`
	Tokens        []Token       `bson:"tokens"           json:"-"`
	Role          int           `bson:"role"             json:"-"`
	Password      string        `bson:"password"         json:"-"`
	Email_address string        `bson:"email_address"    json:"email_address"`
}

type Token struct {
	Token string `bson:"token"    json:"token"`
}

type Book struct {
	Id            bson.ObjectId `bson:"_id"              json:"-"`
	Title         string        `bson:"title"            json:"title"`
	Subtitle      string        `bson:"subtitle"         json:"subtitle"`
	Description   string        `bson:"description"      json:"description"`
	Cover         string        `bson:"cover"            json:"cover"`
	Publisher     string        `bson:"publisher"        json:"publisher"`
	PublishedDate string        `bson:"publishedDate"    json:"publishedDate"`
	ISBN10        string        `bson:"isbn-10"          json:"isbn-10"`
	ISBN13        string        `bson:"isbn-13"          json:"isbn-13"`
	Owner         string        `bson:"owner"            json:"owner"`
	Formats       []Format      `bson:"formats"          json:"formats"`
}

type Format struct {
	Format string `bson:"format"    json:"format"`
	Size   string `bson:"size"      json:"size"`
}

const (
	mongodb_host = "localhost"
	mongodb_db   = "Alexandria"
)

func main() {

	session, err := mgo.Dial(mongodb_host)

	if err != nil {
		panic(err)
	}

	defer session.Close()

	session.SetMode(mgo.Monotonic, true)

	db := session.DB(mongodb_db)

	m := martini.Classic()
	m.Use(render.Renderer())

	m.Get("/books/", func(req *http.Request, r render.Render) {

		user := User{}
		token := req.URL.Query().Get("token")

		n, err := db.C("Users").Find(bson.M{"tokens.token": token}).Count()

		if err != nil {
			panic(err)
		}

		if n == 0 {
			r.JSON(403, nil)
		} else {
			err = db.C("Users").Find(bson.M{"tokens.token": token}).One(&user)

			if err != nil {
				panic(err)
			}

			result := []Book{}

			fmt.Println(user.Id.Hex())

			err = db.C("Books").Find(bson.M{"owner": user.Id.Hex()}).All(&result)

			if err != nil {
				panic(err)
			}

			r.JSON(200, result)
		}

	})

	m.Run()
}
