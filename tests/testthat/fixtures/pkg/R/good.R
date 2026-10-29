#' Compute the weighted mean
#'
#' Uses [weighted.mean()]. The `scale_colour_hue()` alias and "Colour Theory"
#' keep their spelling.
#'
#' @param x A numeric vector.
#' @param w If `NULL`, the default, all weights are 1.
#' @returns A number.
#' @export
good_mean <- function(x, w = NULL) {
  weighted.mean(x, w)
}

#' @export
print.good <- function(x, ...) {
  invisible(x)
}

#' Example data
#'
#' @format A data frame.
"example_data"

#' Add two plots
#'
#' @param e1,e2 Plots.
#' @returns A plot.
#' @rdname plot-add
#' @export
"+.myplot" <- function(e1, e2) e1
