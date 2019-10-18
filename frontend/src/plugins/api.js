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

      //console.log(categories, counts);
      return result.data;
    } catch (err) {
      return {error: "something went wrong", details: JSON.stringify(err)}
    }
}

export async function suggestions(str, vocab) {
  try {
    const params = {
      vocab: vocab,
      text_so_far: str
    };
    const result = await axios.get("/api/autocomplete", {params});
    
  
    return result.data;
  } catch (err) {
    return [str];
  }
}