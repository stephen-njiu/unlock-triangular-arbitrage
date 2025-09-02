# Get all possible traingular arbitrage cycles from the filtered pairs, forward pass only!
# O(n^2) complexity
def triangular_cycles(filtered_pairs, limit):
    cycles = set()
    triangular_cycles = []

    for pair in filtered_pairs[:limit]:
        token1_a = pair['token0']['symbol']
        token1_b = pair['token1']['symbol']
        pair_a = pair['pair']
        token1_a_id = pair['token0']['id']
        token1_b_id = pair['token1']['id']
        contract1_a = pair['id']
        token1_a_decimals = pair['token0']['decimals']
        token1_b_decimals = pair['token1']['decimals']
        token1_a_price = pair['token0Price']
        token1_b_price = pair['token1Price']

        # find second pair which has token1_a or token1_b
        for pair in filtered_pairs:
            box_b = []
            if pair['pair'] != pair_a:
                token2_a = pair['token0']['symbol']
                token2_b = pair['token1']['symbol']
                pair_b = pair['pair']
                token2_a_id = pair['token0']['id']
                token2_b_id = pair['token1']['id']
                contract2_a = pair['id']
                token2_a_decimals = pair['token0']['decimals']
                token2_b_decimals = pair['token1']['decimals']
                token2_a_price = pair['token0Price']
                token2_b_price = pair['token1Price']

                # if token2_a in box_a or token2_b in box_a:
                if token1_b == token2_a or token1_b == token2_b:
                    box_b.append(token1_a)
                    box_b.append(token1_b)
                    box_b.append(token2_a)
                    box_b.append(token2_b)
                    box_b.append(pair_a)
                    box_b.append(pair_b)

                    # find third pair which has token1_a or token1_b
                    for pair in filtered_pairs:
                        box_c = []
                        if pair['pair'] != pair_a and pair['pair'] != pair_b:
                            token3_a = pair['token0']['symbol']
                            token3_b = pair['token1']['symbol']
                            pair_c = pair['pair']
                            token3_a_id = pair['token0']['id']
                            token3_b_id = pair['token1']['id']
                            contract3_a = pair['id']
                            token3_a_decimals = pair['token0']['decimals']
                            token3_b_decimals = pair['token1']['decimals']
                            token3_a_price = pair['token0Price']
                            token3_b_price = pair['token1Price']
                            if token3_a in box_b and token3_b in box_b and token3_a != token3_b:
                                box_c.append(token3_a)
                                box_c.append(token3_b)
                                if (pair_a, pair_b, pair_c) not in cycles:# and token1_a in box_c:
                                    cycles.add((pair_a, pair_b, pair_c))
                                    combined = pair_a + "." + pair_b + "."+ pair_c
                                    # print(f"Cycle found: {pair_a} -> {pair_b} -> {pair_c}")
                                    return_dict = {
                                        'pair_a':pair_a,
                                        'pair_a_base':token1_a,
                                        'pair_a_quote':token1_b,
                                        'pair_b':pair_b,
                                        'pair_b_base':token2_a,
                                        'pair_b_quote':token2_b,
                                        'pair_c':pair_c,
                                        'pair_c_base':token3_a,
                                        'pair_c_quote':token3_b,
                                        'combined':combined,
                                        'token1_base_id':token1_a_id,
                                        'token1_quote_id':token1_b_id,
                                        'token2_base_id':token2_a_id,
                                        'token2_quote_id':token2_b_id,
                                        'token3_base_id':token3_a_id,
                                        'token3_quote_id':token3_b_id,
                                        'contract1':contract1_a,
                                        'contract2':contract2_a,
                                        'contract3':contract3_a,
                                        'token1_base_decimals':token1_a_decimals,
                                        'token1_quote_decimals':token1_b_decimals,
                                        'token2_base_decimals':token2_a_decimals,
                                        'token2_quote_decimals':token2_b_decimals,
                                        'token3_base_decimals':token3_a_decimals,
                                        'token3_quote_decimals':token3_b_decimals,
                                        'token1_base_price':token1_a_price,
                                        'token1_quote_price':token1_b_price,
                                        'token2_base_price':token2_a_price,
                                        'token2_quote_price':token2_b_price,
                                        'token3_base_price':token3_a_price,
                                        'token3_quote_price':token3_b_price,   
                                    }
                                    triangular_cycles.append(return_dict)

            
    return triangular_cycles
