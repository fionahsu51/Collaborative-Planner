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
        task_list: [],
        me: "",
        make_addition: "F",
        errors: [],
        days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.check_form = function () {
        // This checks the form for an empty title or unchosen day.
        app.vue.errors = [];

        if (!app.vue.new_task_title) {
            app.vue.errors.push("Title required.");
        }

        if (!app.vue.new_task_day) {
            app.vue.errors.push("Day required.");
        }
    };

    app.add_task = function () {
        app.check_form();
        if (!app.vue.errors.length) {
            const message = { title: app.vue.new_task_title, description: app.vue.new_task_description, day_selected: app.vue.new_task_day };
            axios.post("../create_task", message).then(function() {
                app.vue.new_task_title = "";
                app.vue.new_task_description = "";
                app.get_all_tasks();
                location.reload();
            });
        }
    };

    app.get_all_tasks = function () {
        axios.get(get_tasks_url)
            .then(function (response){
                app.vue.task_list = response.data.r;
                app.vue.me = response.data.me;
            });
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        add_task: app.add_task,
        get_all_tasks: app.get_all_tasks,
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
        app.get_all_tasks()
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
