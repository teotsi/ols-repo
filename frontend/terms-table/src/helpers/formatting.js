/**
 * Helper that injects a key property to each term in the list.
 * Required by ant.d
 * @param {*} terms the list of terms to map
 * @returns a list of terms with a "key" property injected
 */
export const formatTermData = (terms) => terms.map((term) => ({ ...term, key: term.id }));
