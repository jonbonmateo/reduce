import React from 'react';
import { connect } from 'react-redux';

const SongDetail = ({mySelectedSong}) => {

    if( !mySelectedSong) {
        return(
            <div>
                Please select a song
            </div>
        );
    }

    return(
        <div>
            <h3>Details fors:</h3>
            <p><b>Title:</b> {mySelectedSong.title} </p>
            <p><b>Author:</b> {mySelectedSong.author}  </p>
            <p><b>Duration:</b> {mySelectedSong.duration} </p>
            
        </div>
    );
};

const mapStateToProps = (state) => {
  return { mySelectedSong: state.selectedSong };
};


export default connect(mapStateToProps)(SongDetail);