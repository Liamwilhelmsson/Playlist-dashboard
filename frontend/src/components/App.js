import React, { useState } from "react";
import { render } from "react-dom";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import { LoginPage } from "./Loginpage";
import { Homepage } from "./Homepage";
import { ProtectedRoute } from "./ProtectedRoute";
import { createTheme, ThemeProvider } from "@material-ui/core";

const theme = createTheme({
  palette: {
    primary: {
      main: "#9fd9af",
      contrastText: "#000000",
    },
    secondary: {
      main: "#F6A8A6",
      contrastText: "#696969",
    },
  },
  typography: {
    fontFamily: "Arial",
  },
});

const App = (props) => {
  const [authentication, setAuthentication] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    // Check if authenticated and update state
    const response = await fetch("/api/is-authenticated");
    const json = await response.json();
    setAuthentication(json.is_authenticated);
    setLoading(false);
  };

  fetchData();

  // Renter empty if authentication check not done
  if (loading) {
    return <div></div>;
  }

  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Switch>
          <Route exact path="/login" component={LoginPage} />
          <ProtectedRoute
            exact
            authenticated={authentication}
            path="/"
            component={Homepage}
          />
        </Switch>
      </BrowserRouter>
    </ThemeProvider>
  );
};

render(<App />, document.getElementById("app"));

export default App;
