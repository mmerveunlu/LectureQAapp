import torch


MODEL_CLASSES = {
    "bert": (BertConfig, BertForQuestionAnswering, BertTokenizer),
    "camembert": (CamembertConfig, CamembertForQuestionAnswering, CamembertTokenizer),
    "roberta": (RobertaConfig, RobertaForQuestionAnswering, RobertaTokenizer),
    "xlnet": (XLNetConfig, XLNetForQuestionAnswering, XLNetTokenizer),
    "xlm": (XLMConfig, XLMForQuestionAnswering, XLMTokenizer),
    "distilbert": (DistilBertConfig, DistilBertForQuestionAnswering, DistilBertTokenizer),
    "albert": (AlbertConfig, AlbertForQuestionAnswering, AlbertTokenizer),
}


class MyArguments():
    def __init__(self,args_dict):
        self.data_dir = args_dict["data_dir"]
        self.model_name_or_path = args_dict["model_name_or_path"]
        self.max_seq_length = args_dict["max_seq_length"]
        self.predict_file = args_dict["predict_file"]
        self.version_2_with_negative = args_dict["version_2_with_negative"]
        self.max_query_length = args_dict["max_query_length"]
        self.threads = args_dict["threads"]
        self.doc_stride = args_dict["doc_stride"]
        self.local_rank = args_dict["local_rank"]
        self.n_gpu = args_dict["n_gpu"]
        self.per_gpu_eval_batch_size = args_dict["per_gpu_eval_batch_size"]
        self.eval_batch_size = args_dict["eval_batch_size"]
        self.output_dir = args_dict["output_dir"]
        self.model_type = args_dict["model_type"]
        

def load_and_cache_examples(args, tokenizer):
    """ """ 

    # Load data features from cache or dataset file
    input_dir = args.data_dir if args.data_dir else "."
    cached_features_file = os.path.join(
        input_dir,
        "cached_{}_{}_{}".format(
            "dev" if evaluate else "train",
            list(filter(None, args.model_name_or_path.split("/"))).pop(),
            str(args.max_seq_length),
        ),
    )

    logger.info("Creating features from dataset file at %s", input_dir)

    processor = SquadV2Processor() if args.version_2_with_negative else SquadV1Processor()

    examples = processor.get_dev_examples(args.data_dir, filename=args.predict_file)


    features, dataset = squad_convert_examples_to_features(
        examples=examples,
        tokenizer=tokenizer,
        max_seq_length=args.max_seq_length,
        doc_stride=args.doc_stride,
        max_query_length=args.max_query_length,
        is_training=not evaluate,
        return_dataset="pt",
        threads=args.threads,
    )

    logger.info("Saving features into cached file %s", cached_features_file)
    torch.save({"features": features, "dataset": dataset, "examples": examples}, cached_features_file)

    return dataset


def predict_on(args, model, tokenizer, prefix=""):
    """ """ 

    dataset, examples, features = load_and_cache_examples(args, tokenizer)

    if not os.path.exists(args.output_dir) and args.local_rank in [-1, 0]:
        os.makedirs(args.output_dir)

    args.eval_batch_size = args.per_gpu_eval_batch_size * max(1, args.n_gpu)

    # Note that DistributedSampler samples randomly
    eval_sampler = SequentialSampler(dataset)
    eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=args.eval_batch_size)

    # Eval!
    logger.info("***** Running prediction {} *****".format(prefix))
    logger.info("  Num examples = %d", len(dataset))
    logger.info("  Batch size = %d", args.eval_batch_size)

    all_results = []
    start_time = timeit.default_timer()

    for batch in tqdm(eval_dataloader, desc="Evaluating"):
        model.eval()
        batch = tuple(t.to(args.device) for t in batch)

        with torch.no_grad():
            inputs = {
                "input_ids": batch[0],
                "attention_mask": batch[1],
                "token_type_ids": batch[2],
            }

            if args.model_type in ["xlm", "roberta", "distilbert", "camembert", "bart", "longformer"]:
                del inputs["token_type_ids"]

            feature_indices = batch[3]
            outputs = model(**inputs)

        for i, feature_index in enumerate(feature_indices):
            eval_feature = features[feature_index.item()]
            unique_id = int(eval_feature.unique_id)

            output = [to_list(output[i]) for output in outputs.to_tuple()]

            start_logits, end_logits = output
            result = SquadResult(unique_id, start_logits, end_logits)

            all_results.append(result)

    evalTime = timeit.default_timer() - start_time
    logger.info("  Evaluation done in total %f secs (%f sec per example)", evalTime, evalTime / len(dataset))

    # Compute predictions
    output_prediction_file = os.path.join(args.output_dir, "predictions_{}.json".format(prefix))
    output_nbest_file = os.path.join(args.output_dir, "nbest_predictions_{}.json".format(prefix))

    if args.version_2_with_negative:
        output_null_log_odds_file = os.path.join(args.output_dir, "null_odds_{}.json".format(prefix))
    else:
        output_null_log_odds_file = None

    predictions = compute_predictions_logits(
            examples,
            features,
            all_results,
            args.n_best_size,
            args.max_answer_length,
            args.do_lower_case,
            output_prediction_file,
            output_nbest_file,
            output_null_log_odds_file,
            args.verbose_logging,
            args.version_2_with_negative,
            args.null_score_diff_threshold,
            tokenizer,
    )

    # Compute the F1 and exact scores.
    # results = squad_evaluate(examples, predictions)
    # return results
    return 


def run_predict_on_model():
    args_dict = { "data_dir":"",
                  "model_name_or_path":"experiments/bert-large-cased-whole-word-masking-finetuned-squad_batch4_epoch16_seq256-eng-exp1",
                  "max_seq_length":256,
                  "predict_file":"",
                  "version_2_with_negative":False,
                  "max_query_length":64,
                  "threads":1,
                  "doc_stride":128,
                  "local_rank":"",
                  "n_gpu":1,
                  "per_gpu_eval_batch_size":1,
                  "eval_batch_size":1,
                  "output_dir":"",
                  "model_type":"bert"
    }
    
    args = MyArguments(args_dict)

    args.model_type = args.model_type.lower()
    config_class, model_class, tokenizer_class = MODEL_CLASSES[args.model_type]
    config = config_class.from_pretrained(args.model_name_or_path)
    
    tokenizer = tokenizer_class.from_pretrained(args.model_name_or_path,
                                                do_lower_case=args.do_lower_case)
    model = model_class.from_pretrained(
        args.model_name_or_path,
        from_tf=bool(".ckpt" in args.model_name_or_path),
        config=config)

    args_dict["data_dir"]

    predict_on(args, model, tokenizer)


if __name__ == "__init__":
    run_predict_on_model()
