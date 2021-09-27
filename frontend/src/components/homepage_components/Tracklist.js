import React, { useState, useEffect } from "react";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import { FixedSizeList } from "react-window";
import {
  ListItemAvatar,
  Avatar,
  Box,
  makeStyles,
  Typography,
} from "@material-ui/core";

const useStyles = makeStyles((theme) => {
  return {
    listScroll: {
      "&::-webkit-scrollbar": {
        width: "0.4em",
      },
      "&::-webkit-scrollbar-track": {
        "-webkit-box-shadow": "inset 0 0 6px rgba(0,0,0,0.3)",
      },
      "&::-webkit-scrollbar-thumb": {
        backgroundColor: "rgba(192, 236, 204, 1)",
      },
    },
  };
});

const renderRow = ({ data, style, index }) => {
  const track = data[index];
  return (
    <ListItem style={style} key={index} component="div">
      <ListItemAvatar>
        <Avatar alt={track.trackName} src={track.albumCover} />
      </ListItemAvatar>
      <ListItemText primary={track.trackName} secondary={track.artistName} />
    </ListItem>
  );
};

export const TrackList = ({ tracks }) => {
  const classes = useStyles();
  return (
    tracks && (
      <Box
        sx={{
          width: "100%",
          height: 800,
          maxWidth: 360,
          bgcolor: "background.paper",
        }}
      >
        <Typography variant="h6">Tracks</Typography>
        <FixedSizeList
          height={800}
          width={360}
          itemSize={65}
          itemCount={tracks.length}
          overscanCount={5}
          itemData={tracks}
          className={classes.listScroll}
          sx={{}}
        >
          {renderRow}
        </FixedSizeList>
      </Box>
    )
  );
};
