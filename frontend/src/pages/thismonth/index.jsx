import React, { useState, useEffect } from 'react';
import { NavBar } from '../../components/Navbar'
import { SongsList } from '../../components/SongsList'
import styles from '../../styles'
import { renderDefaultPage } from '../../components/DefaultPage';
import { Tabs } from '../../components/Tabs';

let url = 'http://localhost:8000/thismonth'

export const ThisMonth = () => {

    const[songs, setSongs] = useState([]);
    const[userInfo, setUserInfo] = useState([]);


    const dateTransform = (date) => {
        let year = date.getFullYear();
        let month = date.getMonth() + 1;
        let dt = date.getDate();
        let dateString = `${year}-${month}-${dt}`;
        return dateString;
    }


    const songsApi = async(url, dateString) => {
        const response  = await fetch(`${url}${dateString}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },    
        })
        const data = await response.json();
        return data;
    }

    const selectspecificDate = (sdate,edate) => {
        sdate = new Date(sdate);
        edate = new Date(edate);
        const startDate = dateTransform(sdate);
        const endDate = dateTransform(edate);

        console.log(startDate, endDate)

        let dateString = '';
        if(sdate && edate){
            dateString = `?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`
        }

        songsApi(url, dateString)
        .then(data => {
            setSongs(data["message"]);
            setUserInfo(data["user_info"]);
        }).catch(error => {
            console.error(error);
        });
    }

    useEffect(() => {
        songsApi(url, '')
        .then(data => {
            setSongs(data["message"]);
            setUserInfo(data["user_info"]);
        }).catch(error => {
            console.error(error);
        });
    }, []);


    return(
        <div className={`bg-black w-full overflow-hidden `}>
            <div className={`${styles.flexCenter}`}>
                <div className={`w-full bg-gradient-to-r bg-slate-900`}>
                    <NavBar data={userInfo} select={selectspecificDate}/>
                </div>
            </div>
            <div className='w-full bg-gradient-to-r bg-slate-900'>
                <Tabs />    
            </div>
            <div className={`bg-gradient-to-t h-dvh  bg-slate-900 ${styles.paddingX} ${styles.flexStart}`}>
                <div className={`${styles.boxWidth} `}>
                    {songs && songs.length > 0 ? (
                        <SongsList data={songs} />
                    ) : (
                        renderDefaultPage()
                    )}
                </div>
            </div>
        </div>
    );
}