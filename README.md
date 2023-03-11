# Pull Request Labeler
A minor action which assigns labels to pull requests based off of the base
branch. For instance, if a pull request is being made into `main`, then it will
assign the label `Target: main` to the pull request. If the label corresponding
to the base branch does not exist, then the label will neither be created nor
applied.


*Uses [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html)*


