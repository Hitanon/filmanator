import { makeAutoObservable } from "mobx";


class UserStore {
    constructor({
        email = "",
        history = [""],
        liked_titles = [""],
        dislike_titles = [""],
        prefered_genres = [""],
        active_tab = 'history'
    } = {}) {
        this.data = {
            email,
            history,
            liked_titles,
            dislike_titles,
            prefered_genres,
            active_tab
        }
        makeAutoObservable(this);
    }

    setEmail(email) {
        this.data.email = email;
    }

    get email() {
        return this.data.email;
    }

    setActiveTab(active_tab) {
        this.data.active_tab = active_tab;
    }

    get active_tab() {
        return this.data.active_tab;
    }
}


const userStore = new UserStore({
    email: 'test_email@email.com'
});

export default userStore;