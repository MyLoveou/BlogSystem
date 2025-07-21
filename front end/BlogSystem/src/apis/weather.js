import request from "@/utils/request.js"

export const getWeatherData = () => {
  return request.get("/weather/get_by_location/", { params: { location: "101200101" } })
}