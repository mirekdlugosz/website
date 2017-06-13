const smooth_scroll_to = (target_elem, duration=700) => {
	let smooth_step = (start_time, end_time, now) => {
		if (now <= start_time) { return 0; }
		if (now >= end_time) { return 1; }
		let x = (now - start_time) / (end_time - start_time);
		return x*x*(3 - 2*x);
	}

    if (typeof target_elem === 'undefined') {
        target_elem = document.getElementById(window.location.hash.slice(1));
    }

    let navbar_offset = document.getElementById('navbar-main').offsetHeight;
    let target = Math.max(0, target_elem.offsetTop - navbar_offset);
	let start_position = window.scrollY;
    let previous_position = start_position;
	let distance = target - start_position;
	let start_time = Date.now();
	let end_time = start_time + duration;

	return new Promise((resolve, reject) => {
		const scroll_frame = () => {
            if (window.scrollY !== previous_position) {
                reject("interrupted");
                return;
            }

			let move_factor = smooth_step(start_time, end_time, Date.now());
			let current_position = Math.round(start_position + (distance * move_factor));
            document.body.scrollTop = current_position;

            if (current_position === target) {
                resolve();
                return;
            }

			previous_position = current_position;
			setTimeout(scroll_frame, 0);
		}

		setTimeout(scroll_frame, 0);
	});
}

window.addEventListener("load", () => {
    if (window.location.hash === "" || window.location.hash === "#about") {
        window.location.hash = "";
    } else {
        smooth_scroll_to();
    }

    document.querySelectorAll("#navbar-main ul li a").forEach(elem => {
        elem.addEventListener("click", () => {
            event.preventDefault();
            smooth_scroll_to(document.getElementById(elem.hash.slice(1)));
        });
    });
});
