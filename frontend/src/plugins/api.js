import axios from "axios";

/**
 * Get 
 * @param {*} first_list 
 * @param {*} second_list 
 */
export async function search(first_list, second_list) {
    try {
      const params = { first_list: first_list, second_list: second_list };
      
      const result = await axios.post("/api/query", params);

      const categories = [];
      const counts = [];

      for (const [cat, count] of Object.entries(result.data)) {
        counts.push([count]);
        categories.push([cat]);
      }

      //console.log(categories, counts);
      return {categories: categories, counts: counts};
    } catch (err) {
      return {error: "something went wrong", details: JSON.stringify(err)}
    }
}

export async function suggestions(str, vocab) {
  try {
    const params = {

    };
    //const result = await axios.get("/api/autocomplete", params);

  
    return ["Measles", "Europe", "Russia"];
  } catch (err) {
    return [str];
  }
}