const express = require("express");
const users_router = require("./routes/users/users-router");

const api = express();
api.use("/user", users_router);

module.exports = api;
