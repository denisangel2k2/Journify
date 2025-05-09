import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';

import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';


import { Navigation, Pagination, FreeMode } from 'swiper/modules';

const HistoryJournalSongs = ({ journal }) => {
    return (
        <div className='history-journal-songs'>
            <Swiper
                modules={[Navigation, Pagination, FreeMode]}
                navigation={true}
                pagination={{ clickable: true }}
                className="myHistoryJournalSongsSwiper"
                slidesPerView={1}
                spaceBetween={50}
                history={{ key: 'slide', }}
            >
                {journal.questions.map((question) => (
                    <SwiperSlide>
                        <div className="journal-history-song">
                            {question.img &&
                                <>  
                                    <img src={question.img} alt={`Song cover for ${question.answer}`}></img>
                                    <p className='quote'>{question.question}</p>
                                    <p>Answer: {question.answer}</p>
                                    <p>Emotion: {question.emotion}</p>
                                </>
                            }
                            {!question.img && 
                            <>
                                <div className='img-placeholder'>No cover art for song found</div>
                                <p className='quote'>{question.question}</p>
                                <p>You haven't matched a song to this quote.</p>    
                            </>}

                        </div>
                    </SwiperSlide>
                ))}


            </Swiper>
        </div>
    );
}
export default HistoryJournalSongs;