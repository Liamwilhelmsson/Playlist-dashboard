import React from "react";
import { Button, makeStyles } from "@material-ui/core";

const useStyles = makeStyles({
  button: {
    background:
      "linear-gradient(0deg, rgba(192,236,204,1) 0%, rgba(159,217,175,1) 100%)",
    borderRadius: "5em",
    color: "#000000",
    height: 42,
    width: 150,
    boxShadow: "0 3px 5px 2px rgba(111,129,116,1)",
  },
});

export const LogoutButton = () => {
  const classes = useStyles();
  return (
    <Button className={classes.button} variant="contained" onClick={logout}>
      Log out
    </Button>
  );
};

// Logout spotify user
const logout = () => {
  const requestoptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  };

  fetch("/api/logout", requestoptions).then((response) =>
    window.location.replace("/")
  );
};
