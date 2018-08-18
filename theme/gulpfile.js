var gulp = require("gulp");
var sass = require("gulp-sass");
var autoprefixer = require("gulp-autoprefixer")
var cleanCSS = require("gulp-clean-css");
var concat = require("gulp-concat");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");

// Compile SCSS
gulp.task('css:compile', function() {
    return gulp.src([
        './src/scss/variables.scss',
        './src/scss/bootstrap.scss',
        './src/scss/fontawesome.scss',
        './src/scss/pygments.scss',
        './vendor/Lora/style.scss',
        './src/scss/style.scss',
    ])
        .pipe(concat('style.scss'))
        .pipe(sass.sync({
            outputStyle: 'expanded'
        }).on('error', sass.logError))
        .pipe(autoprefixer('last 2 versions'))
        .pipe(gulp.dest('./static/css'))
});

// Minify CSS
gulp.task('css:minify', ['css:compile'], function() {
    return gulp.src([
        './static/css/**/*.css',
        '!./static/css/**/*.min.css'
    ])
        .pipe(concat('style.css'))
        .pipe(cleanCSS())
        .pipe(rename({
            suffix: '.min'
        }))
        .pipe(gulp.dest('./static/css'));
});

// CSS
gulp.task('css', ['css:compile', 'css:minify']);

// Minify JavaScript
gulp.task('js:minify', function() {
    return gulp.src([
        './node_modules/bootstrap.native/dist/bootstrap-native-v4.min.js',
        './src/js/*.js'
    ])
        .pipe(concat('script.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('./static/js'));
});

// JS
gulp.task('js', ['js:minify']);

// copy FontAwesome font files
gulp.task('fonts', function() {
    return gulp.src([
        './node_modules/@fortawesome/fontawesome-free/webfonts/*',
        './vendor/Lora/*',
        '!./vendor/Lora/style.scss'
    ])
        .pipe(gulp.dest('./static/fonts'));
});

// copy images
gulp.task('images', function() {
    return gulp.src([
        './src/img/*'
    ])
        .pipe(gulp.dest('./static/img'));
});

// Default task
gulp.task('default', ['css', 'js', 'fonts', 'images']);

// Dev task
gulp.task('dev', ['default'], function() {
    gulp.watch('./src/**/*.scss', ['css']);
    gulp.watch('./src/**/*.js', ['js']);
});
