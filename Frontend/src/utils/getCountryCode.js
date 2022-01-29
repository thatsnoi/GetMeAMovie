import axios from 'axios'

const getCountryCode = async () => {
  try {
    const response = await axios.get('https://ipapi.co/json')
    return response.data.country_code
  } catch (error) {
    console.log(error)
    return 'ES'
  }
}

export default getCountryCode
