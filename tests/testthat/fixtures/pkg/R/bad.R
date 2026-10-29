#' Creates The Weighted Mean Of A Vector.
#'
#' This uses \code{\link{weighted.mean}} and keeps the colour.
#'
#' @param x numeric vector of values
#' @param w weights, defaults to NULL
#' @export
wmean <- function(x, w = NULL) {
  weighted.mean(x, w)
}

#' Compute a summary that has a title which runs well past the limit of chars
#'
#' @param x A vector.
#' @returns A number.
#' @export
long_title <- function(x) x

#' Subtract two plots
#'
#' @param e1,e2 Plots.
#' @export
"-.myplot" <- function(e1, e2) e1
