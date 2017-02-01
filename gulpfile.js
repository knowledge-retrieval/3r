var gulp = require('gulp');
var ghPages = require('gulp-gh-pages');

gulp.task('docs:deploy', function() {
  return gulp.src('./site/**/*')
    .pipe(ghPages());
});
