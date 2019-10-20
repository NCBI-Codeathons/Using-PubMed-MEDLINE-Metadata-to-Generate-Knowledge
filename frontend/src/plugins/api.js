import axios from "axios";

/**
 * Execute terms search
 * @param {*} primary_terms Primary search terms
 * @param {*} refinement_terms Refinement search terms
 */
export async function search(primary_terms, refinement_terms) {
    try {
      gtag('event', 'search', {primary: primary_terms, refinement: refinement_terms});
      const params = { first_list: primary_terms, second_list: refinement_terms };
      const result = await axios.post("/api/query", params);
      return result.data;
    } catch (err) {
      gtag('event', 'search_failed', {primary: primary_terms, refinement: refinement_terms, error: err});
      return {error: "something went wrong", details: JSON.stringify(err)}
    }
}

/**
 * Get autocompletion suggestion list
 * @param {String} str Entered string
 * @param {String} vocab primary or refinement vocabulary.
 */
export async function suggestions(str, vocab) {
  try {
    const params = {
      vocab: vocab,
      text_so_far: str
    };
    gtag('event', 'suggestions', {str: str, vocab: vocab});
    const result = await axios.get("/api/autocomplete", {params});
    return result.data;
  } catch (err) {
    return [str];
  }
}