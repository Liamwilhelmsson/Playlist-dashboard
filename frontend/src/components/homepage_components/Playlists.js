import React, { useState, useEffect } from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import { ListItemAvatar, Avatar } from "@material-ui/core";

export const Playlists = ({ currentPlaylist, setCurrentPlaylist }) => {
  const [playlists, setPlaylists] = useState([]);
  useEffect(() => {
    // Fetch playlists and update state
    fetch("/api/playlists")
      .then((response) => response.json())
      .then((data) => {
        // If playlists found
        if (data.playlists.length) {
          setPlaylists(data.playlists);
          setCurrentPlaylist(data.playlists[0]);
        }
      });
  }, []);

  return (
    playlists && (
      <List dense>
        {playlists.map((playlist) => (
          <ListItem
            key={playlist.id}
            button
            onClick={() => setCurrentPlaylist(playlist)}
          >
            <ListItemAvatar>
              <Avatar alt={playlist.name} src={playlist.icon} />
            </ListItemAvatar>
            <ListItemText primary={playlist.name} />
          </ListItem>
        ))}
      </List>
    )
  );
};
