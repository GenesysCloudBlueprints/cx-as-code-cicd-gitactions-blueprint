variable "classifier_queue_names" {
  type        = list(string)
  description = "The list of queues names to create."
}

variable "classifier_queue_members" {
  type        = list(string)
  description = "The member to assign to the queue"
}

