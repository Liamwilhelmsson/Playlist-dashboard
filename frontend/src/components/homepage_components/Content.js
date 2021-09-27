import React, { useState, useEffect } from "react";
import { Grid, Container, Typography, Box } from "@material-ui/core";
import { ActiveShapePieChart } from "./Charts/ActiveShapePieChart";
import { TrackList } from "./Tracklist";
import { VerticalComposedChart } from "./Charts/VeticalComposedChart";
import { CustomAreaChart } from "./Charts/CustomAreaChart";
import { CustomRadarChart } from "./Charts/CustomRadarChart";
import { CustomRadialBarChart } from "./Charts/CustomRadialBarChart";

export const Content = ({ currentPlaylist }) => {
  const [playlistData, setPlaylistData] = useState({
    artistCount: null,
    tracks: null,
    genresCount: null,
    tracksPerBpm: null,
    audioCharactersticsAverage: null,
    tracksPerDecade: null,
  });

  useEffect(() => {
    // Fetch playlists and update state
    fetch("/api/playlist-data" + "?playlist_id=" + currentPlaylist.id)
      .then((response) => response.json())
      .then((data) => {
        setPlaylistData(data.playlistData);
      });
  }, [currentPlaylist]);

  return (
    <div>
      <Container maxWidth="xl" style={{ margin: "0 0 0 0" }}>
        <Grid container>
          <Grid item sm={12} md={3}>
            <TrackList tracks={playlistData.tracks} />
          </Grid>
          <Grid item container sm={12} md={9}>
            <Grid item xs={12} sm={12} md={4}>
              <Typography align="center">Genres</Typography>
              <VerticalComposedChart data={playlistData.genresCount} />
            </Grid>
            {/* TODO: look here for inspo http://organizeyourmusic.playlistmachinery.com/#  Top tracks per playlist? Return top tracks loop and compare until 3 tracks are found*/}
            <Grid item xs={12} sm={12} md={8}>
              <Typography align="center">Bpm</Typography>
              <CustomAreaChart data={playlistData.tracksPerBpm} />
            </Grid>
            <Grid item xs={12} sm={12} md={4}>
              <CustomRadarChart
                data={playlistData.audioCharactersticsAverage}
              />
            </Grid>
            <Grid item xs={12} sm={12} md={4}>
              <Box marginTop={4}>
                <Typography align="center">Tracks per artist</Typography>
              </Box>
              <ActiveShapePieChart data={playlistData.artistCount} />
            </Grid>
            <Grid item xs={12} sm={12} md={4}>
              <Box marginTop={4}>
                <Typography align="center">Tracks per decade</Typography>
              </Box>
              <CustomRadialBarChart data={playlistData.tracksPerDecade} />
            </Grid>
          </Grid>
        </Grid>
      </Container>
    </div>
  );
};
