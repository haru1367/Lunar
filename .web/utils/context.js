import { createContext, useState } from "react"
import { Event, hydrateClientStorage, useEventLoop } from "/utils/state.js"

export const initialState = {"auth_state": {"confirm_password": "", "day": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"], "month": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], "password": "", "time_valid_confirm_password": true, "time_valid_email_address": true, "time_valid_password": true, "time_valid_user_birthday_day": true, "time_valid_user_birthday_month": true, "time_valid_user_birthday_year": true, "time_valid_user_password": false, "time_valid_user_realname": false, "time_valid_username": true, "user_birthday_day": "", "user_birthday_day_valid": false, "user_birthday_month": "", "user_birthday_month_valid": false, "user_birthday_year": "", "user_birthday_year_valid": false, "user_confirm_password_valid": false, "user_email_address": "", "user_email_address_valid": false, "user_find_id_day": "", "user_find_id_email": "", "user_find_id_month": "", "user_find_id_name": "", "user_find_id_year": "", "user_find_password_day": "", "user_find_password_email_address": "", "user_find_password_id": "", "user_find_password_month": "", "user_find_password_year": "", "user_password_valid": false, "user_realname": "", "user_realname_valid": false, "username": "", "year": ["1960", "1961", "1962", "1963", "1964", "1965", "1966", "1967", "1968", "1969", "1970", "1971", "1972", "1973", "1974", "1975", "1976", "1977", "1978", "1979", "1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]}, "home_state": {"KAKAO_REST_API_KEY": "", "aichatting": [], "calculate_dday": {}, "checked": false, "crater": "", "craters": [], "daylist": [], "dday_content": "", "dday_date": "", "dday_day": 0, "dday_month": 0, "dday_year": 0, "ddaylist": [], "df": {"columns": [], "data": []}, "distance": "", "end_location_x": "", "end_location_y": "", "files": [], "followers": [], "following": [], "friend": "", "gpt_chat_daylist": [], "image": "", "img": [], "imgshow": false, "kakaotalk": "", "map_count": 1, "map_hotplaces": [], "map_html": "/map.html", "map_iframe": "", "map_search_input": "", "memo_content": "", "memo_show": false, "messages": [], "month": 2, "month_str": {"1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June", "7": "July", "8": "August", "9": "September", "10": "October", "11": "November", "12": "December"}, "music_chart_info": [], "path_time": "", "popup_day": "", "popup_memo": "", "popup_video_title": "", "popup_video_url": "", "receive_user": "User", "recorded_memo": [], "saved_music_results": [], "saved_video_results": [], "search": "", "search_calendar": "", "search_month": "February", "search_singer": "", "search_singer_result": [], "search_users": [], "search_video": "", "show": false, "start_location_x": "", "start_location_y": "", "status_atmospheric_pressure": "", "status_climate": "", "status_climate_icon_url": "", "status_feel_temperature": "", "status_humidity": "", "status_temperature": "", "status_wind_direction": "", "status_wind_speed": "", "taxi_fee": "", "time_map_iframe": "<iframe src=\"/map.html\" width=\"100%\" height=\"500px\"></iframe>", "today_max_temperature": "", "today_min_temperature": "", "toll_fee": "", "user_input_chat": "", "weather_message_result": [], "weather_search": "", "weather_search_show": false, "year": 2024, "youtube_results": []}, "is_hydrated": false, "logged_in": false, "router": {"session": {"client_token": "", "client_ip": "", "session_id": ""}, "headers": {"host": "", "origin": "", "upgrade": "", "connection": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": ""}, "page": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}}, "user": null}

export const ColorModeContext = createContext(null);
export const StateContext = createContext(null);
export const EventLoopContext = createContext(null);
export const clientStorage = {"cookies": {}, "local_storage": {}}

export const initialEvents = () => [
    Event('state.hydrate', hydrateClientStorage(clientStorage)),
]

export const isDevMode = true

export function EventLoopProvider({ children }) {
  const [state, addEvents, connectError] = useEventLoop(
    initialState,
    initialEvents,
    clientStorage,
  )
  return (
    <EventLoopContext.Provider value={[addEvents, connectError]}>
      <StateContext.Provider value={state}>
        {children}
      </StateContext.Provider>
    </EventLoopContext.Provider>
  )
}