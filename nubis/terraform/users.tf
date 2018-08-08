resource "aws_iam_user" "nagios" {
  name = "${var.service_name}-${var.environment}-nagios"
  path = "/applicaton/${var.service_name}/"
}

resource "aws_iam_access_key" "nagios" {
  user = "${aws_iam_user.nagios.name}"
}

resource "aws_iam_user_policy" "nagios" {
  name = "nagios-bucket-access"
  user = "${aws_iam_user.nagios.name}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
          "${module.nagios.arn}",
          "${module.nagios.arn}/*"
      ]
    }
  ]
}
EOF
}
