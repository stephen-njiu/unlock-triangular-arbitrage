def calculate_surface_arb(real_dict, start_amount, min_surface_rate):
    surface_dict = {}
    final_coin = ''
    d1, d2, d3 = '', '', '' # direction of trade for each swap

    pair_a = real_dict['pair_a']
    pair_b = real_dict['pair_b']
    pair_c = real_dict['pair_c']

    pair_a_base = real_dict['pair_a_base']
    pair_a_quote = real_dict['pair_a_quote']
    pair_b_base = real_dict['pair_b_base']
    pair_b_quote = real_dict['pair_b_quote']
    pair_c_base = real_dict['pair_c_base']
    pair_c_quote = real_dict['pair_c_quote']

    pair_a_base_id = real_dict['token1_base_id']
    pair_a_quote_id = real_dict['token1_quote_id']
    pair_b_base_id = real_dict['token2_base_id']
    pair_b_quote_id = real_dict['token2_quote_id']
    pair_c_base_id = real_dict['token3_base_id']
    pair_c_quote_id = real_dict['token3_quote_id']

    combined = real_dict['combined']

    # address info
    contract_a = real_dict['contract1']
    contract_b = real_dict['contract2']
    contract_c = real_dict['contract3']

    acquired_coin_t1 = 0
    acquired_coin_t2 = 0
    acquired_coin_t3 = 0

    swap_1_rate = 0
    swap_2_rate = 0
    swap_3_rate = 0

    swap_1_rate = real_dict['token1_quote_price']
    c1 = pair_a_base_id

    acquired_coin_t1 = start_amount * swap_1_rate if swap_1_rate != 0 else 0 # forward swap
    d1 = 'baseToQuote'
    c2 = pair_a_quote_id
    if pair_a_quote == pair_b_base:
        swap_2_rate = real_dict['token2_quote_price']
        acquired_coin_t2 = acquired_coin_t1 * swap_2_rate if swap_2_rate != 0 else 0 # forward swap
        final_coin = pair_b_quote
        c3= pair_b_quote_id
        d2 = 'baseToQuote'
    elif pair_a_quote == pair_b_quote:
        swap_2_rate = real_dict['token2_base_price']
        acquired_coin_t2 = acquired_coin_t1 * swap_2_rate if swap_2_rate != 0 else 0 # reverse swap
        final_coin = pair_b_base
        c3= pair_b_base_id
        d2 = 'quoteToBase'
    else:
        print("Error in pair_a and pair_b matching")
        print(combined, pair_a_base, pair_a_quote, pair_b_base, pair_b_quote, 'stage2Error')
        return
    
    if final_coin == pair_c_base:
        swap_3_rate = real_dict['token3_quote_price']
        acquired_coin_t3 = acquired_coin_t2 * swap_3_rate if swap_3_rate != 0 else 0 # forward swap
        c4= pair_c_quote_id
        d3 = 'baseToQuote'
    elif final_coin == pair_c_quote:
        swap_3_rate = real_dict['token3_base_price']
        acquired_coin_t3 = acquired_coin_t2 * swap_3_rate if swap_3_rate != 0 else 0 # reverse swap
        c4= pair_c_base_id
        d3 = 'quoteToBase'
    else:
        print("Error in pair_b and pair_c matching")
        print(combined, pair_b_base, pair_b_quote, pair_c_base, pair_c_quote, 'stage3Error')
        return
    
    # Profit and Loss Calculations
    profit_loss = acquired_coin_t3 - start_amount
    profit_loss_perc = (profit_loss / start_amount) * 100 if profit_loss != 0 else 0

    valid_coins = acquired_coin_t1 != 0 and acquired_coin_t2 != 0 and acquired_coin_t3 != 0
    if profit_loss_perc >= min_surface_rate and valid_coins:
        # print(f"{combined}: {c1} -> {c2} -> {c3} -> {c4} \t Profit/Loss: {profit_loss:.6f} ({profit_loss_perc:.2f}%)")
        # print(f"{combined}: {pair_a_base} -> {pair_a_quote} -> {final_coin} -> {pair_a_base} \t Profit/Loss: {profit_loss:.6f} ({profit_loss_perc:.2f}%)")

        surface_dict = {  
            "swap1": pair_a_base,
            "swap2": pair_a_quote,
            "swap3": final_coin,
            "poolContract1": contract_a,
            "poolContract2": contract_b,
            "poolContract3": contract_c,
            "poolDirectionTrade1": d1,
            "poolDirectionTrade2": d2,
            "poolDirectionTrade3": d3,
            "startingAmount": start_amount,
            "acquiredCoinT1": acquired_coin_t1,
            "acquiredCoinT2": acquired_coin_t2,
            "acquiredCoinT3": acquired_coin_t3,
            "swap1Rate": swap_1_rate,
            "swap2Rate": swap_2_rate,
            "swap3Rate": swap_3_rate,
            "profitLoss": profit_loss,
            "profitLossPerc": profit_loss_perc,
            "direction": "forward",
            "tradeDesc1": f"Start with {pair_a_base} of {start_amount}. Swap at {swap_1_rate} for {pair_a_quote} acquiring {acquired_coin_t1}.",
            "tradeDesc2": f"Swap {acquired_coin_t1} of {pair_a_quote} at {swap_2_rate} for {final_coin} acquiring {acquired_coin_t2}.",
            "tradeDesc3": f"Swap {acquired_coin_t2} of {final_coin} at {swap_3_rate} for {pair_a_base} acquiring {acquired_coin_t3}."
        }

    return surface_dict
