function __localStorage() {
    this.setItem = function(key, value) {
        $.cookie(key, value, {expires: 30});
    }
    this.getItem = function(key) {
        return $.cookie(key);
    }
}
if (localStorage === undefined) {
    localStorage = new __localStorage();
}