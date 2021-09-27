import React, { useState, useEffect } from "react";
import { Button, makeStyles } from "@material-ui/core";
import { Redirect } from "react-router";

export const LoginPage = () => {
  const [authentication, setAuthentication] = useState(false);

  useEffect(() => {
    // Fetch from api and update authentication state
    fetch("/api/is-authenticated")
      .then((response) => response.json())
      .then((data) => {
        setAuthentication(data.is_authenticated);
      });
  }, []);

  // If logged in redirect back to homepage else render login button
  return authentication ? (
    <Redirect to="/" />
  ) : (
    <div className="background">
      <div className="center">
        <LoginButton />
      </div>
    </div>
  );
};

const useStyles = makeStyles({
  button: {
    background: "#84d29a",
    borderRadius: "5em",
    border: 0,
    color: "#000000",
    height: 48,
    padding: "0 20px",
    boxShadow: "0 3px 5px 2px rgba(111,129,116,1)",
  },
});

const LoginButton = () => {
  const classes = useStyles();
  return (
    <Button
      variant="contained"
      color="primary"
      className={classes.button}
      onClick={() => {
        // Fetch and launch spotify-auth url
        fetch("/api/login")
          .then((response) => response.json())
          .then((data) => window.location.replace(data.url));
      }}
    >
      Log in with spotify
    </Button>
  );
};
