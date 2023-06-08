// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        new_task_title: "",
        new_task_description: "",
        new_task_day: "",
        new_task_month: "",
        new_task_date: "",
        new_task_year: "",
        new_task_js_date: new Date(),
        new_task_invited_user: "", 
        new_task_invited_users: [],
        new_task_uninvited_users: [],
        users: [],

        errors: [],
        task_list: [],
        
        me: "",
        make_addition: "F",

        months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        dates: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"],
        years: ["2023", "2024", "2025", "2026", "2027"],
        days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        current_day: new Date().getDay(),
        current_view: "week",
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => { 
            e._idx = k++; 
        });
        return a;
    };

    app.get_users = function () {
        axios.get(get_users_url)
            .then(function (response){
                let users = response.data.users;
                app.enumerate(users);
                app.vue.users = users;
                app.vue.me = response.data.me;
            });
    };

    app.check_form = function () {
        // This checks the form for an empty title or unchosen day.
        app.vue.errors = [];

        if (!app.vue.new_task_title) {
            app.vue.errors.push("Title required.");
        }

        app.vue.new_task_js_date = new Date(app.vue.new_task_month + " " + app.vue.new_task_date + ", " + app.vue.new_task_year + " " + "00:00:00");
        if (Object.prototype.toString.call(app.vue.new_task_js_date) === "[object Date]") {
            if (isNaN(app.vue.new_task_js_date.getTime())) {
                app.vue.errors.push("Invalid date.");

            // Checks for valid February dates.
            } else if (app.vue.new_task_js_date.getFullYear() != app.vue.new_task_year || app.vue.months[app.vue.new_task_js_date.getMonth()] != app.vue.new_task_month || app.vue.new_task_js_date.getDate() != app.vue.new_task_date) {
                app.vue.errors.push("Invalid date.");
            }
        } else {
            app.vue.errors.push("Invalid date.");
        }
    };

    app.get_day_from_date = function (date) {
        // This returns a weekday (0 = Sunday, ..., 6=Saturday) given a Date() object.
        // Algorithm from https://www.hackerearth.com/blog/developers/how-to-find-the-day-of-a-week/
        let t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4];
        let m = date.getMonth();
        let y = date.getFullYear(); 
        y -= (m + 1) < 3;
        return ((y + Math.floor(y/4) - Math.floor(y/100) + Math.floor(y/400) + t[m] + date.getDate()) % 7);
    };
    
    app.add_task = function () {
        // This adds a task using data from the form fields.
        app.check_form();
        if (!app.vue.errors.length) {
            const message = { 
                title: app.vue.new_task_title, 
                description: app.vue.new_task_description,
                date: [parseInt(app.vue.new_task_year, 10), app.vue.new_task_js_date.getMonth() + 1, parseInt(app.vue.new_task_date, 10)],
                day: app.vue.days[app.get_day_from_date(app.vue.new_task_js_date)],
                invited_users: app.vue.new_task_invited_user.id,
            };
            axios.post("../create_task", message).then(function () {
                app.vue.new_task_title = "";
                app.vue.new_task_description = "";
                app.get_all_tasks();
            });
        }
    };
    
    app.set_invite = function(u_idx, s) {
        let user = app.vue.users[u_idx]; // map to the right place in users list
        user.status = s; // set its status
        axios.post(invite_url, {user_id: user.id, status: s});
        // reset_invited_list();
    };

    function reset_invited_list() {
        app.vue.new_task_invited_users = [];
        app.vue.new_task_uninvited_users = [];
        for (let u of app.vue.users) {
            if (u.status) {
                app.vue.new_task_invited_users.push(u)
            } else {
                app.vue.new_task_uninvited_users.push(u)
            }
        }
    }

    app.previous = function () {
        // This goes to the previous day/week/month of the view.
        if (app.vue.current_view === 'day') {
            app.vue.current_day -= 1;
            if (app.vue.current_day < 0) {
                app.vue.current_day = 6;
            }
        }
    };

    app.today = function () {
        // This goes to the current day/week/month of the view.
        if (app.vue.current_view === 'day') {
            app.vue.current_day = new Date().getDay();
        }
    };

    app.next = function () {
        // This goes to the next day/week/month of the view.
        if (app.vue.current_view === 'day') {
            app.vue.current_day = (app.vue.current_day + 1) % 7;
        }
    };

    app.get_all_tasks = function () {
        // This grabs all of the tasks from the database.
        axios.get(get_tasks_url)
            .then(function (response) {
                app.vue.task_list = response.data.r;
                app.vue.me = response.data.me;
            });
    };
    
    app.check_invited_users = function () {

    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        get_day_from_date: app.get_day_from_date,
        add_task: app.add_task,
        previous: app.previous,
        today: app.today,
        next: app.next,
        get_all_tasks: app.get_all_tasks,
        check_invited_users: app.check_invited_users,
        get_users: app.get_users,
        set_invite: app.set_invite,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
        app.get_all_tasks();
        app.get_users();
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
