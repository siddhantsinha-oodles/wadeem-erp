$(() => {
	class ProgramListing {
		constructor() {
			this.bind_search();
		}

		bind_search() {
			$('input[type=search]').on('keydown', (e) => {
				if (e.keyCode === 13) {
					// Enter
					const value = e.target.value;
					if (value) {
						window.location.search = 'search=' + e.target.value;
					} else {
						window.location.search = '';
					}
				}
			});
		}

	}

	new ProgramListing();

	function get_query_string(object) {
		const url = new URLSearchParams();
		for (let key in object) {
			const value = object[key];
			if (value) {
				url.append(key, value);
			}
		}
		return url.toString();
	}

	function if_key_exists(obj) {
		let exists = false;
		for (let key in obj) {
			if (obj.hasOwnProperty(key) && obj[key]) {
				exists = true;
				break;
			}
		}
		return exists ? obj : undefined;
	}
});
