import {
  AppBar,
  Box,
  Drawer,
  Grid,
  makeStyles,
  Toolbar,
  Typography,
} from "@material-ui/core";
import React, { useState, useEffect } from "react";
import { Playlists } from "./homepage_components/Playlists";
import { LogoutButton } from "./homepage_components/LogoutButton";
import { Content } from "./homepage_components/Content";

const drawerWidth = 270;
const appbarHeight = 64;

const useStyles = makeStyles((theme) => {
  return {
    root: {
      display: "flex",
      width: "100%",
    },

    appbar: {
      height: appbarHeight,
      width: `calc(100% - ${drawerWidth}px)`,
    },

    drawer: {
      width: drawerWidth,
    },

    drawPaper: {
      width: drawerWidth,
      background:
        "linear-gradient(0deg, rgba(192,236,204,1) 0%, rgba(159,217,175,1) 100%)",
      "&::-webkit-scrollbar": {
        display: "none",
      },

      "-ms-overflow-style": "none" /* IE and Edge */,
      scrollbarWidth: "none" /* Firefox */,
    },

    page: {
      background: "#FFFFFF",
      width: "100%",
      height: "100%",
      flexGrow: 1,
    },

    toolbar: {
      height: appbarHeight,
      padding: "16px",
    },
  };
});

export const Homepage = () => {
  const classes = useStyles();
  const [currentPlaylist, setCurrentPlaylist] = useState(null);

  // Remove #_=_ from url when redirect by facebook login
  if (window.location.hash === "#_=_") {
    history.replaceState
      ? history.replaceState(null, null, window.location.href.split("#")[0])
      : (window.location.hash = "");
  }

  return (
    <div className={classes.root}>
      {/* Tool bar */}
      <AppBar className={classes.appbar} position="fixed">
        <Toolbar>
          <Grid justifyContent="space-between" alignItems="center" container>
            <Grid item>
              {currentPlaylist && (
                <Typography variant="h6">{currentPlaylist.name}</Typography>
              )}
            </Grid>

            <Grid item>
              <LogoutButton />
            </Grid>
          </Grid>
        </Toolbar>
      </AppBar>

      {/* Side bar */}
      <Drawer
        className={classes.drawer}
        variant="permanent"
        anchor="left"
        classes={{ paper: classes.drawPaper }}
      >
        <Box mt={2} ml={2}>
          <Typography variant="h6">Playlists</Typography>
        </Box>
        <Playlists
          currentPlaylist={currentPlaylist}
          setCurrentPlaylist={setCurrentPlaylist}
        />
      </Drawer>

      {/* Content */}
      <div className={classes.page}>
        <div className={classes.toolbar} />
        {currentPlaylist && <Content currentPlaylist={currentPlaylist} />}
      </div>
    </div>
  );
};
