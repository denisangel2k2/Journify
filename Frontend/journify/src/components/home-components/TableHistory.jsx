import React from "react";
import JournalHistoryItem from "./JournalHistoryItem";
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/free-mode';
import 'swiper/css/pagination';

import { Navigation } from 'swiper/modules';

const TableHistory = ({ setIsHistoryModalVisible, history, setCurrentSelectedJournal }) => {
    return (
        <div className="table-history">
            <Swiper
                modules={[Navigation]}
                slidesPerView={7}
                freeMode={true}
                pagination={{ clickable: true }}
                className="mySwiper"
            >

                {history.map((journal) =>
                (
                    <SwiperSlide>
                        <JournalHistoryItem journal={journal} onClick={() => { setCurrentSelectedJournal(journal); setIsHistoryModalVisible(true) }} />
                    </SwiperSlide>)
                )}
            </Swiper>
        </div>

    );
};
export default TableHistory;
